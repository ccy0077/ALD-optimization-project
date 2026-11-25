# ALD 공정 조건 최적화를 위한 탐색 알고리즘 비교
가상 품질 함수에서 Grid, Random, local GP Bayesian Optimization 비교. 실제 ALD 장비 데이터가 아니다.

## 실행
Python 3.13 환경에서 저장소 루트에서 실행:
```sh
python -m pip install -r requirements.txt
python experiments/run.py
python experiments/plot.py
```
results 폴더에 CSV 및 PNG 생성. seed 0~29, 차원 2/3/4, 예산 50/100/200/500. Random과 BO는 500회 경로의 prefix를 사용하고 Grid는 예산별 독립 격자. Grid 반복은 결정론적이라 품질 SD가 0이다. hit99는 최초 99점 도달 횟수이며 미도달은 budget+1로 기록. 시간은 순차 실행의 누적 perf_counter 기준이며 환경에 따라 변동한다.

## 구현
src/search.py: 가상 함수 및 세 탐색법. BO는 최근접 32개 관측으로 GP를 구성하고 EI를 128개 후보에서 최대화한다. NumPy/SciPy의 행렬연산과 정규 CDF 사용. 외부 코드를 복사하지 않았다. ChatGPT가 코드, 실험 실행, 분석 및 보고서 초안을 생성했다. 제출자는 검토와 재실행 및 자기 판단 추가가 필요하다.
