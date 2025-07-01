# Use Cases

Login/Register/Logout
Timeout for HTTP/gRPC traffic.
Retry for HTTP/gRPC traffic.

# Requirements (functional/non-functional)

functional
- O sistema deve permitir que users façam authenticação através de username e password.
- Apenas users autenticados podem criar tópicos e fazer publicações.

non-functional
- As credenciais devem ser armazenadas de forma segura e nunca circular em texto em claro.
- Pedidos entre serviços devem ter timeout configurado (ex: 30 segundos) para evitar atrasos elevados.
- Retries devem ser limitados a no máximo 3 tentativas por pedido para evitar overload.
- use Firebase Authentication (Google Cloud) for the Login/Register actions
- use Service Mesh with Istio to introduce the Timeout and Retry logic for HTTP/gRPC traffic

# Deployment plan

(May 7 - May 14)
- Phase 7
- finish some work discussed (e.g. ingress).
    - Ingress; configmaps e secrets; Resources e probes; Deploy automatico; Cluster; Curl.
- polish the code.
- start implementing the new cloud related improvements to the existing project.
(May 14 - May 28) - Phase 8
- finish implementing the new cloud related improvements to the existing project.