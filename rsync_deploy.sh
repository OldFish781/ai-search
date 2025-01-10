#!/bin/bash

# 定义源和目标路径
SOURCE="./"
DESTINATION="zentao_lan200:/weique/ai-search/"
#DESTINATION="turing-vpn-ssh-111:/weique/edward/fine-tuning/LLaMA-Factory-main/"
EXCLUDE_FILE="./.exclude"

# 定义 rsync 选项
OPTIONS="-avz --progress --update"

# 检查排除文件是否存在
if [ -f "$EXCLUDE_FILE" ]; then
    OPTIONS="$OPTIONS --exclude-from=$EXCLUDE_FILE"
else
    echo "警告：排除文件 $EXCLUDE_FILE 不存在，将同步所有文件。"
fi

# 执行 rsync
echo "开始同步..."
rsync $OPTIONS $SOURCE $DESTINATION

# 检查 rsync 执行结果
if [ $? -eq 0 ]; then
    echo "同步成功完成。"
else
    echo "同步过程中出现错误，请检查日志。"
fi