import pandas as pd
from typing import List, Dict


class KLineProcessor:
    """K线数据处理类，用于识别K线图中的顶分型和底分型，并确定笔的端点


    该类实现了金融技术分析中K线数据的预处理、包含关系处理、分型识别和笔的确定等功能，
    是构建技术分析图表的基础工具。
    """

    def __init__(self, df: pd.DataFrame):
        """初始化KLineProcessor实例并进行数据验证

        Args:
            df: 包含K线数据的DataFrame，必须包含'trade_date', 'high', 'low'列

        Raises:
            ValueError: 当输入数据缺少必要列时抛出
        """
        self._validate_input(df)
        self.data = df.copy()
        self.kline = []
        self.fractals = []
        self.lines = []

    @staticmethod
    def _validate_input(df: pd.DataFrame) -> None:
        """验证输入数据的合法性

        Args:
            df: 待验证的K线数据

        Raises:
            ValueError: 当缺少必要列时抛出
        """
        required_columns = {'trade_date', 'high', 'low'}
        if not required_columns.issubset(df.columns):
            missing_columns = required_columns - set(df.columns)
            raise ValueError(f"输入数据缺少必要列: {missing_columns}")

    def _preprocess_data(self) -> List[Dict]:
        """预处理K线数据，添加分型标记列

        Returns:
            预处理后的K线数据列表，每个元素为包含K线信息的字典
        """
        self.data['Fmark'] = 0
        self.data['Fval'] = 0.0
        kline = [row.to_dict() for _, row in self.data.iterrows()]

        for k in kline:
            k['Fmark'] = 0
            k['Fval'] = None
            k['line'] = None

        return kline

    def _handle_merged_kline(self, kline: List[Dict]) -> List[Dict]:
        """处理K线图中的包含关系

        Args:
            kline: 原始K线数据列表

        Returns:
            处理包含关系后的K线数据列表
        """
        if len(kline) < 2:
            return kline

        new_kline = kline[:2]

        for i in range(2, len(kline)):
            current_kline = kline[i]
            prev_two = new_kline[-2:]
            k1, k2 = prev_two[0], prev_two[1]

            # 确定处理方向
            direction = 1 if k2['high'] >= k1['high'] else -1

            cur_high, cur_low = current_kline['high'], current_kline['low']
            last_high, last_low = k2['high'], k2['low']

            # 检查是否存在包含关系
            if (cur_high <= last_high and cur_low >= last_low) or (cur_high >= last_high and cur_low <= last_low):
                if direction == 1:  # 向上处理
                    new_high = max(last_high, cur_high)
                    high_date = k2['high_date'] if new_high == last_high and k2.get('high_date') else k2[
                        'trade_date'] if new_high == last_high else current_kline['trade_date']

                    new_low = max(last_low, cur_low)
                    low_date = k2['low_date'] if new_low == last_low and k2.get('low_date') else k2[
                        'trade_date'] if new_low == last_low else current_kline['trade_date']

                elif direction == -1:  # 向下处理
                    new_high = min(last_high, cur_high)
                    high_date = k2['high_date'] if new_high == last_high and k2.get('high_date') else k2[
                        'trade_date'] if new_high == last_high else current_kline['trade_date']

                    new_low = min(last_low, cur_low)
                    low_date = k2['low_date'] if new_low == last_low and k2.get('low_date') else k2[
                        'trade_date'] if new_low == last_low else current_kline['trade_date']
                else:
                    raise ValueError("无效的处理方向")

                # 更新当前K线数据
                current_kline['high'] = new_high
                current_kline['low'] = new_low
                current_kline['high_date'] = high_date
                current_kline['low_date'] = low_date
                new_kline.pop(-1)

            new_kline.append(current_kline)

        return new_kline

    def _identify_fractals(self, kline: List[Dict]) -> List[Dict]:
        """识别K线图中的顶分型和底分型

        Args:
            kline: 处理过包含关系的K线数据

        Returns:
            识别出的分型列表，每个元素包含分型日期、类型和值
        """
        fractals = []

        for i in range(1, len(kline) - 1):
            k_prev, k_current, k_next = kline[i - 1], kline[i], kline[i + 1]

            # 识别顶分型
            if k_prev['high'] < k_current['high'] > k_next['high']:
                k_current['Fmark'] = 1
                k_current['Fval'] = k_current['high']
                k_current['trade_date'] = k_current['high_date'] if k_current.get('high_date') else k_current[
                    'trade_date']
                fractals.append({
                    'trade_date': k_current['trade_date'],
                    'Fmark': k_current['Fmark'],
                    'Fval': k_current['Fval']
                })

            # 识别底分型
            if k_prev['low'] > k_current['low'] < k_next['low']:
                k_current['Fmark'] = -1
                k_current['Fval'] = k_current['low']
                k_current['trade_date'] = k_current['low_date'] if k_current.get('low_date') else k_current[
                    'trade_date']
                fractals.append({
                    'trade_date': k_current['trade_date'],
                    'Fmark': k_current['Fmark'],
                    'Fval': k_current['Fval']
                })

        return fractals

    def _determine_lines(self, fractals: List[Dict], kline: List[Dict]) -> List[Dict]:
        """基于分型确定技术分析中的笔

        Args:
            fractals: 识别出的分型列表
            kline: 原始K线数据

        Returns:
            确定的笔端点列表，按时间排序
        """
        if not fractals:
            return []

        sorted_fractals = sorted(fractals, key=lambda x: x['trade_date'])
        lines = [sorted_fractals[0]]

        for i in range(1, len(sorted_fractals)):
            current_fractal = sorted_fractals[i]
            last_line = lines[-1]

            # 同类型分型处理
            if last_line['Fmark'] == current_fractal['Fmark']:
                if (last_line['Fmark'] == 1 and last_line['Fval'] < current_fractal['Fval']) or \
                        (last_line['Fmark'] == -1 and last_line['Fval'] > current_fractal['Fval']):
                    lines.pop()
                    lines.append(current_fractal)
            else:
                # 不同类型分型处理
                if (last_line['Fmark'] == 1 and current_fractal['Fval'] >= last_line['Fval']) or \
                        (last_line['Fmark'] == -1 and current_fractal['Fval'] <= last_line['Fval']):
                    lines.pop()
                    continue

                # 检查中间K线数量
                between_kline = [k for k in kline if
                                 last_line['trade_date'] <= k['trade_date'] <= current_fractal['trade_date']]
                if len(between_kline) >= 5:
                    lines.append(current_fractal)

                    # 检查笔的有效性
                    max_high = max(k['high'] for k in between_kline)
                    min_low = min(k['low'] for k in between_kline)

                    if (last_line['Fmark'] == -1 and current_fractal['Fval'] < max_high) or \
                            (last_line['Fmark'] == 1 and current_fractal['Fval'] > min_low):
                        lines.pop()

        return lines

    def process_kline(self) -> pd.DataFrame:
        """处理K线数据，识别分型和笔并标注到原始数据

        Returns:
            标注了分型和笔的K线数据DataFrame
        """
        # 数据预处理
        self.kline = self._preprocess_data()

        # 处理包含关系
        processed_kline = self._handle_merged_kline(self.kline)

        # 识别分型
        self.fractals = self._identify_fractals(processed_kline)

        # 确定笔
        self.lines = self._determine_lines(self.fractals, processed_kline)

        # 将笔的信息标注到原始数据
        for line in self.lines:
            mask = self.data['trade_date'] == line['trade_date']
            self.data.loc[mask, 'Fmark'] = line['Fmark']
            self.data.loc[mask, 'Fval'] = line['Fval']

        self.lines = pd.DataFrame(self.lines)

        # 进一步处理分型标记
        self._assign_fractal_flags()

        # 数据类型转换
        self._convert_data_types()

        return self.data

    def _assign_fractal_flags(self):
        """分配分型标记"""
        # 第一次遍历：设置临时标记
        flag = 0
        for i in range(len(self.data)):
            if self.data.at[i, 'Fmark'] != 0:
                flag = self.data.at[i, 'Fmark']
                continue
            if flag == -1:
                self.data.at[i, 'Fmark'] = 2
            elif flag == 1:
                self.data.at[i, 'Fmark'] = -2

        # 第二次遍历：处理第一个笔端点前的数据
        if not self.lines.empty:
            first_line_date = self.lines.iloc[0]['trade_date']
            first_line_type = self.lines.iloc[0]['Fmark']
            mask = self.data['trade_date'] < first_line_date
            self.data.loc[mask, 'Fmark'] = -2 if first_line_type == -1 else 2

        # 标记转换
        self.data['Fmark'] = self.data['Fmark'].replace({
            1: 0,  # 顶分型笔端点
            -1: 1,  # 底分型笔端点
            -2: 3  # 非笔端点分型
        })

    def _convert_data_types(self) -> None:
        """转换数据类型，优化存储和计算"""
        dtype_mapping = {
            'trade_date': 'datetime64[ns]',
            'open': 'float32',
            'high': 'float32',
            'low': 'float32',
            'close': 'float32',
            'Fmark': 'int8',
            'Fval': 'float32'
        }

        # 只转换存在的列
        existing_columns = {col: dtype for col, dtype in dtype_mapping.items() if col in self.data.columns}
        if existing_columns:
            self.data = self.data.astype(existing_columns)

    def get_processed_data(self) -> pd.DataFrame:
        """获取处理后的K线数据，包含分型和笔的标注

        Returns:
            处理后的K线数据DataFrame
        """
        return self.process_kline()


