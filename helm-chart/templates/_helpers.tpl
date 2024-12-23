
{{/* 네임스페이스 */}}
{{- define "AppNameSpace" -}}
  {{- default "stock" .Values.global.namespace -}}
{{- end -}}

{{/* 카프카 브로커 주소 */}}
{{- define "kafkaBrokerAddress" -}}
  {{ .Values.global.kafka_broker_address }}
{{- end -}}

{{/* ECR 레지스트리 넘버 */}}
{{- define "ecrNumber" -}}
  {{ .Values.global.ecrNumber }}
{{- end -}}

{{/* 실시간 호가 데이터 토픽 이름 */}}
{{- define "hokaTopic" -}}
  {{ .Values.global.HOKA_TOPIC }}
{{- end -}}

{{/* 실시간 체결가 데이터 토픽 이름 */}}
{{- define "conclusionTopic" -}}
  {{ .Values.global.CONCLUSION_TOPIC }}
{{- end -}}

{{/* Stock APP 프로듀서 레플리카 갯수*/}}
{{- define "producerReplica" -}}
  {{- default "1" .Values.producer.replicaCount -}}
{{- end -}}

{{/* Stock APP 한투 API 종목 코드*/}}
{{- define "producerStockCode" -}}
  {{ .Values.producer.stockCode }}
{{- end -}}

{{/* Stock APP 한투 API KEY*/}}
{{- define "producerAppKey" -}}
  {{ .Values.producer.appKey }}
{{- end -}}

{{/* Stock APP 한투 API SECRET*/}}
{{- define "producerSecret" -}}
  {{ .Values.producer.appSecret }}
{{- end -}}


{{/* Stock APP 컨슈머 레플리카 갯수*/}}
{{- define "consumerReplica" -}}
  {{- default "3" .Values.consumer.replicaCount -}}
{{- end -}}

{{/* InfluxDB Url*/}}
{{- define "influxDBUrl" -}}
  {{ .Values.consumer.influxDBUrl }}
{{- end -}}

{{/* InfluxDB token*/}}
{{- define "influxDBToken" -}}
  {{ .Values.consumer.influxDBToken }}
{{- end -}}