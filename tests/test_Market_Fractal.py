from Chan_Theory.Market_Fractal import  KLineProcessor
import pandas as pd

if __name__ == '__main__':
    # 假设example.csv包含必要的K线数据列
    df = pd.read_csv('example.csv')
    df = df.sort_values('trade_date', ascending=True).reset_index(drop=True)

    processor = KLineProcessor(df)
    processed_data = processor.get_processed_data()
    print(processed_data)