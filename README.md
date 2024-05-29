# MetaGPT-workspace
包括了role定义、action设计以及智能体开发。

环境配置及下载安装参考https://blog.csdn.net/weixin_49206002/article/details/139203512?spm=1001.2014.3001.5501, 在config中配置好api_key后，agent文件复制到workspace下即可运行。

metagpt配置安装：
```bash
conda create -n metagpt_env python=3.10
conda activate metagpt_env
git clone https://github.com/geekan/MetaGPT.git --depth 1 -b main #进入一个有权限的路径克隆，否则就失败
cd MetaGPT
git clone https://github.com/geekan/MetaGPT.git 
cd /your/path/to/MetaGPT
pip install -e .
```
安装好后开始配置api_key
```bash
cd config
cp config2.yaml key.yaml
vim key.yaml
```
配置,智谱接口详情[智谱](https://open.bigmodel.cn/dev/api#glm-4)

```bash
llm:
  api_type: "zhipuai"  # or azure / ollama / groq etc. Check LLMType for more options
  model: "glm-4"  # or gpt-3.5-turbo
  base_url: "https://open.bigmodel.cn/api/paas/v4/chat/completions"  # or forward url / other llm url
  api_key: "YOUR_API_KEY"
```
