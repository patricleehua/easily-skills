> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimaxi.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>

## Submitting Feedback

If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback:

POST https://platform.minimaxi.com/docs/feedback

```json
{
  "path": "/api-reference/voice-cloning-uploadprompt",
  "feedback": "Description of the issue"
}
```

Only submit feedback when you have something specific and actionable to report.

</AgentInstructions>

# 上传示例音频

> 使用本接口上传示例音频文件，使用示例音频将有助于增强语音合成的音色相似度和稳定性。



## OpenAPI

````yaml /api-reference/speech/voice-cloning/api/upload-prompt.json POST /v1/files/upload
openapi: 3.1.0
info:
  title: MiniMax Voice Cloning API
  description: MiniMax Voice Cloning API with support for voice cloning and file upload
  license:
    name: MIT
  version: 1.0.0
servers:
  - url: https://api.minimaxi.com
security:
  - bearerAuth: []
paths:
  /v1/files/upload:
    post:
      tags:
        - Files
      summary: Upload File
      operationId: uploadFile
      parameters:
        - name: Content-Type
          in: header
          required: true
          description: '请求体的媒介类型 `multipart/form-data` '
          schema:
            type: string
            enum:
              - multipart/form-data
            default: multipart/form-datan
      requestBody:
        description: ''
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - purpose
                - file
              properties:
                purpose:
                  type: string
                  description: |-
                    文件使用目的。取值及支持格式如下：
                    - __prompt_audio__: 快速复刻原始文件，（支持mp3、m4a、wav格式）
                  default: prompt_audio
                  enum:
                    - prompt_audio
                  example: prompt_audio
                file:
                  type: string
                  format: binary
                  description: |-
                    需要上传的文件。填写文件的路径地址 

                    支持上传的文件需遵从以下规范：
                    - 上传的音频文件格式需为：mp3、m4a、wav格式
                    - 上传的音频文件的时长小于8s
                    - 上传的音频文件大小需不超过20mb
        required: true
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UploadFileResp'
components:
  schemas:
    UploadFileResp:
      type: object
      properties:
        file:
          $ref: '#/components/schemas/FileObject'
        base_resp:
          $ref: '#/components/schemas/UploadFileBaseResp'
      example:
        file:
          file_id: ${file_id}
          bytes: 5896337
          created_at: 1700469398
          filename: sample.mp3
          purpose: prompt_audio
        base_resp:
          status_code: 0
          status_msg: success
    FileObject:
      type: object
      properties:
        file_id:
          type: integer
          format: int64
          description: 文件的唯一标识符
        bytes:
          type: integer
          format: int64
          description: 文件大小，以字节为单位
        created_at:
          type: integer
          format: int64
          description: 创建文件时的 Unix 时间戳，以秒为单位
        filename:
          type: string
          description: 文件的名称
        purpose:
          type: string
          description: 文件的使用目的
          default:
            - prompt_audio
    UploadFileBaseResp:
      type: object
      properties:
        status_code:
          type: integer
          description: |-
            状态码及其分别含义如下：
            - 0，请求成功
            - 1002，触发限流，请稍后再试
            - 1004，账号鉴权失败，请检查 API-Key 是否填写正确
            - 1008，账号余额不足
            - 1026，图片描述涉及敏感内容
            - 2013，传入参数异常，请检查入参是否按要求填写
            - 2049，无效的api key

            更多内容可查看错误码查询列表了解详情
        status_msg:
          type: string
          description: 状态详情
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |-
        `HTTP: Bearer Auth`
         - Security Scheme Type: http
         - HTTP Authorization Scheme: Bearer API_key，用于验证账户信息，可在 [账户管理>接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key) 中查看。

````