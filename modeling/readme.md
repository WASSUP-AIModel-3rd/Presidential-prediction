## Modeling
```
Social(사회지표/후보자 정보를 사용한 시계열 CNN)
Text(연설문 본문을 사용한 LSTM)
Importance(토픽 모델링으로 뽑은 주제별 중요도를 사용한 다층 퍼셉트론)

Combined = Social + Text + Importance (세 모델의 출력층 직전 결과를 concatenate 한 뒤 Dense 레이어로 출력하는 모델)
```

- text_classifier_candidate: 후보자 정보 포함 후보자의 당락을 예측하는 Social 모델 사용(최종)
- text_classifier: 후보자 정보 없이 다음 정당만을 예측하는 Social 모델 사용(데이터 전처리와 합본)