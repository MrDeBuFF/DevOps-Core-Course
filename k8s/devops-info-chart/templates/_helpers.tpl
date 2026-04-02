{{- define "devops-info-chart.fullname" -}}
{{ .Release.Name }}-devops-info
{{- end }}

{{- define "devops-info-chart.labels" -}}
app: devops-info
{{- end }}