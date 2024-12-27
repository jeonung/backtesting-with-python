import os

import pandas as pd


def read_market_data(name):
    """주식 시장 데이터를 읽어와 하나의 DataFrame으로 합치는 함수.

    Args:
        name (str): 읽어올 데이터의 이름 (예: "adjprc", "mcap").

    Returns:
        pandas.DataFrame: 합쳐진 데이터 DataFrame. 파일이 없을 경우 빈 DataFrame 반환.
        혹은 파일 입출력 예외 발생시 None 반환.
    """
    try:
        data = pd.DataFrame()
        for year in range(2016, 2022):
            for market in ["kospi", "kosdaq"]:
                file_path = os.path.join("..", "data", f"{name}_{market}_{year}.txt")
                try:
                    tmp = pd.read_table(
                        file_path, sep="\t", names=["Stock", "date", name]
                    )
                    data = pd.concat(
                        [data, tmp], ignore_index=True
                    )  # ignore_index 추가
                except FileNotFoundError:
                    print(f"파일을 찾을 수 없습니다: {file_path}")
                    if data.empty:
                        return (
                            pd.DataFrame()
                        )  # 파일이 하나도 없을 경우 빈 DataFrame 반환
                    continue  # 특정 년도의 파일이 없을 경우 다음 파일로 진행
                except pd.errors.EmptyDataError:
                    print(f"빈 파일입니다: {file_path}")
                    continue
                except Exception as e:
                    print(f"파일 처리 중 오류 발생: {e}")
                    return None  # 그 외 예외 발생시 None 반환

        return data
    except Exception as e:
        print(f"전체적인 함수 실행 중 오류 발생: {e}")
        return None
