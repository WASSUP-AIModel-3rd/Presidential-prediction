# 2024 US Presidential Election Estimator
## Goal(목표): 대선 후보자의 당락 예측

## Methods:
= 사회지표/후보자 개인정보를 사용한 예측 모델(Baseline)
+ 연설문/토론 분석을 기반으로 모델을 추가하여 혼합모델 생성

`
Combined(혼합) = Social(사회지표) + Text(연설문 본문) + Importance(연설문 주제 분포)
`

### Social
- GDP, 소비자 물가지수, 실업률, 현 정권 지지율등의 사회지표 + 후보 정당, 후보 나이, 후보 최종학력 등을 사용하여 후보자 당락 예측

Model: LSTM or Time-Series CNN(최종선정)
- 두 모델 모두 구현
- LSTM
    ```
    (4,10) 입력 -> 64차원 LSTM with 0.3 Dropout -> 1차원 Dense 레이어 출력
    ```

- Time-Series CNN
    - 데이터를 4개씩 묶고 filter size=4인 Conv1D 레이어를 사용해 구현
    ```
    (4,10) 입력 -> 32차원 Conv1D -> 0.3 Dropout -> 64차원 Dense 레이어 -> 1차원 Dense 레이어 출력
    ```

### Text
- 연설문을 100단어씩 쪼개어 사용
```
100차원 입력 -> 128차원 임베딩 레이어 -> 64차원 LSTM 레이어 -> 1차원 Dense 레이어 출력
```

### Importance
- BERTopic 또는 LDA(최종선정)을 사용해 주제 분석 후 분야별로 분류
- 분류한 주제들의 비중을 **중요도**로 간주해 분야별 중요도를 다층 퍼셉트론에 넣어 당락 예측
```
(LDA 6차원, BERTopic 10차원 입력)
x차원 입력 -> 128차원 Dense 레이어 -> Dropout -> 64차원 Dense 레이어 -> 1차원 Dense 레이어 출력
```

### Combined

- 위 3가지 모델의 출력층 직전 결과값(64차원)을 모아 스태킹(Concatenate)
```
192차원 컨캣 레이어 -> 1차원 Dense 레이어 출력
```