# kaldi_sale_collector
カルディのセール情報を収集します

## デプロイ手順

* 秘密鍵をgithubとしてこのディレクトリに置く
* aws.iniにアクセスキーを書く
* github.iniに名前とアドレスを書く
* 「`DOCKER_DEFAULT_PLATFORM=linux/amd64 docker buildx build --provenance=false -t kaldi-sale .`」でビルド
* AWS ECRにpushする（[ここ](https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-ecs-ecr-codedeploy.html)参照）
