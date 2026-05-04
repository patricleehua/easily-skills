> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimaxi.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>

## Submitting Feedback

If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback:

POST https://platform.minimaxi.com/docs/feedback

```json
{
  "path": "/api-reference/voice-cloning-clone",
  "feedback": "Description of the issue"
}
```

Only submit feedback when you have something specific and actionable to report.

</AgentInstructions>

# 音色快速复刻

> 使用本接口进行音色快速复刻。
复刻得到的音色若 7 天内未正式调用，则系统会删除该音色。



## OpenAPI

````yaml /api-reference/speech/voice-cloning/api/openapi.json POST /v1/voice_clone
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
  /v1/voice_clone:
    post:
      tags:
        - Voice
      summary: Voice Clone
      operationId: voiceClone
      requestBody:
        description: Voice clone request parameters
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/VoiceCloneReq'
        required: true
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/VoiceCloneResp'
components:
  schemas:
    VoiceCloneReq:
      type: object
      required:
        - file_id
        - voice_id
      properties:
        file_id:
          type: integer
          format: int64
          description: |-
            待复刻音频的 file_id，通过[文件上传接口](/api-reference/file-management-upload)获得
            上传的待复刻音频文件需遵从以下规范：

            - 上传的音频文件格式需为：mp3、m4a、wav 格式
            - 上传的音频文件的时长最少应不低于 10 秒，最长应不超过 5 分钟
            - 上传的音频文件大小需不超过 20 mb
            - 若使用该参数，则两个子属性（prompt_audio、prompt_text）都为必填项
        voice_id:
          type: string
          description: |-
            克隆音色的 voice_id，正确示例："MiniMax001"。用户进行自定义 voice_id 时需注意：

            - 自定义的 voice_id 长度范围[8,256]
            - 首字符必须为英文字母
            - 允许数字、字母、-、_
            - 末位字符不可为 -、_
            - voice_id 不可与已有 id 重复，否则会报错
        clone_prompt:
          $ref: '#/components/schemas/ClonePrompt'
          description: |-
            音色复刻示例音频，提供本参数将有助于增强语音合成的音色相似度和稳定性。若使用本参数，需同时上传一小段示例音频
            上传的音频文件需遵从以下规范：

            - 上传的音频文件格式需为：mp3、m4a、wav 格式
            - 上传的音频文件的时长小于 8 秒
            - 上传的音频文件大小需不超过 20 mb
        text:
          type: string
          description: >-
            复刻试听参数，限制 1000 字符以内。模型将使用复刻后的音色朗读本段文本内容，并返回试听音频链接。
             注：试听将根据字符数正常收取语音合成费用，定价与 T2A 各接口一致
            - 语气词标签：仅当模型选择 `speech-2.8-hd` 或 `speech-2.8-turbo`
            时，支持在文本中插入语气词标签。支持的语气词：`(laughs)`（笑声）、`(chuckle)`（轻笑）、`(coughs)`（咳嗽）、`(clear-throat)`（清嗓子）、`(groans)`（呻吟）、`(breath)`（正常换气）、`(pant)`（喘气）、`(inhale)`（吸气）、`(exhale)`（呼气）、`(gasps)`（倒吸气）、`(sniffs)`（吸鼻子）、`(sighs)`（叹气）、`(snorts)`（喷鼻息）、`(burps)`（打嗝）、`(lip-smacking)`（咂嘴）、`(humming)`（哼唱）、`(hissing)`（嘶嘶声）、`(emm)`（嗯）、`(whistles)`（口哨）、`(sneezes)`（喷嚏）、`(crying)`（抽泣）、`(applause)`（鼓掌）
        model:
          type: string
          description: 复刻试听参数。指定合成试听音频使用的语音模型，提供 `text` 字段时必传此字段。可选项：
          enum:
            - speech-2.8-hd
            - speech-2.8-turbo
            - speech-2.6-hd
            - speech-2.6-turbo
            - speech-02-hd
            - speech-02-turbo
            - speech-01-hd
            - speech-01-turbo
        language_boost:
          type: string
          description: 是否增强对指定的小语种和方言的识别能力。默认值为 null，可设置为 `auto` 让模型自主判断。
          enum:
            - Chinese
            - Chinese,Yue
            - English
            - Arabic
            - Russian
            - Spanish
            - French
            - Portuguese
            - German
            - Turkish
            - Dutch
            - Ukrainian
            - Vietnamese
            - Indonesian
            - Japanese
            - Italian
            - Korean
            - Thai
            - Polish
            - Romanian
            - Greek
            - Czech
            - Finnish
            - Hindi
            - Bulgarian
            - Danish
            - Hebrew
            - Malay
            - Persian
            - Slovak
            - Swedish
            - Croatian
            - Filipino
            - Hungarian
            - Norwegian
            - Slovenian
            - Catalan
            - Nynorsk
            - Tamil
            - Afrikaans
            - auto
        need_noise_reduction:
          type: boolean
          description: 音频复刻参数，表示是否开启降噪，默认值为 false
          default: false
        need_volume_normalization:
          type: boolean
          description: 音频复刻参数，是否开启音量归一化，默认值为 false
          default: false
        aigc_watermark:
          type: boolean
          description: 是否在合成试听音频的末尾添加音频节奏标识，默认值为 false
          default: false
      example:
        file_id: 123456789
        voice_id: <voice_id>
        clone_prompt:
          prompt_audio: 987654321
          prompt_text: This voice sounds natural and pleasant.
        text: >-
          A gentle breeze sweeps across the soft grass(breath), carrying the
          fresh scent along with the songs of birds.
        model: speech-2.8-hd
        need_noise_reduction: false
        need_volume_normalization: false
        aigc_watermark: false
    VoiceCloneResp:
      type: object
      properties:
        input_sensitive:
          type: object
          description: 输入音频是否命中风控
          properties:
            type:
              type: integer
              description: |-
                输入音频命中风控的类型，取值为以下其一：

                - 0：正常
                - 1：严重违规
                - 2：色情
                - 3：广告
                - 4：违禁
                - 5：谩骂
                - 6：暴恐
                - 7：其他
        demo_audio:
          type: string
          description: 如果请求体中传入了试听文本 text 以及合成试听音频的模型 model，那么本参数将以链接形式返回试听音频，否则本参数为空值
        base_resp:
          $ref: '#/components/schemas/VoiceCloneBaseResponse'
      example:
        input_sensitive: false
        input_sensitive_type: 0
        demo_audio: ''
        base_resp:
          status_code: 0
          status_msg: success
    ClonePrompt:
      type: object
      properties:
        prompt_audio:
          type: integer
          format: int64
          description: 示例音频的 file_id，通过 [文件上传接口](/api-reference/file-management-upload) 获得
        prompt_text:
          type: string
          description: 示例音频的对应文本，需确保和音频内容一致，句末需有标点符号做结尾
    VoiceCloneBaseResponse:
      type: object
      required:
        - status_code
      properties:
        status_code:
          type: integer
          format: int64
          description: |-
            状态码

            - 0: 请求结果正常
            - 1000：未知错误
            - 1001：超时
            - 1002：触发限流
            - 1004：鉴权失败
            - 1013：服务内部错误
            - 2013：输入格式信息不正常
            - 2038：无复刻权限，请检查账号认证状态

            更多内容可查看[错误码查询列表](/api-reference/errorcode)了解详情
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