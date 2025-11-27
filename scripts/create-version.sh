#!/bin/bash

# SQNB 版本管理脚本
set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo "SQNB 版本管理脚本"
    echo ""
    echo "使用方法: $0 <版本号> [选项]"
    echo ""
    echo "示例:"
    echo "  $0 v0.0.2                    # 创建 v0.0.2 版本"
    echo "  $0 v1.0.0 --push             # 创建并推送版本"
    echo "  $0 --current                 # 显示当前版本"
    echo ""
    echo "选项:"
    echo "  --push, -p       创建后自动推送到GitHub"
    echo "  --current, -c    显示当前版本信息"
    echo "  --help, -h       显示此帮助信息"
    echo ""
    echo "版本号格式:"
    echo "  v<主版本>.<次版本>.<修订版本>"
    echo "  示例: v0.0.1, v1.2.3, v2.0.0"
}

# 显示当前版本
show_current_version() {
    if [ -f "version.json" ]; then
        echo "📦 当前版本信息:"
        cat version.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'版本号: {data[\"version\"]}')
print(f'构建时间: {data[\"build_time\"]}')
print(f'Commit: {data[\"commit_hash\"][:8]}')
"
    else
        echo -e "${RED}❌ 未找到 version.json 文件${NC}"
        exit 1
    fi
}

# 验证版本号格式
validate_version() {
    local version=$1
    if [[ ! $version =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo -e "${RED}❌ 版本号格式错误: $version${NC}"
        echo "版本号必须符合格式: v<主版本>.<次版本>.<修订版本>"
        echo "示例: v0.0.1, v1.2.3"
        exit 1
    fi
}

# 主函数
main() {
    local version=""
    local push=false
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--current)
                show_current_version
                exit 0
                ;;
            -p|--push)
                push=true
                shift
                ;;
            -*)
                echo -e "${RED}❌ 未知选项: $1${NC}"
                show_help
                exit 1
                ;;
            *)
                version=$1
                shift
                ;;
        esac
    done
    
    # 检查版本号
    if [ -z "$version" ]; then
        echo -e "${RED}❌ 请提供版本号${NC}"
        show_help
        exit 1
    fi
    
    # 验证版本号格式
    validate_version "$version"
    
    # 检查git状态
    if [ "$push" = true ] && [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}⚠️  工作区有未提交的更改，请先提交更改${NC}"
        git status
        exit 1
    fi
    
    # 创建版本文件
    echo -e "${GREEN}📝 创建版本 $version...${NC}"
    cat > version.json << EOF
{
    "version": "$version",
    "build_time": "$(date -u +"%Y-%m-%d %H:%M:%S")",
    "commit_hash": "$(git rev-parse HEAD)"
}
EOF
    
    # 提交更改
    git add version.json
    git commit -m "🚀 发布版本 $version" || true
    
    # 创建标签
    echo -e "${GREEN}🏷️  创建Git标签 $version...${NC}"
    git tag -f "$version"
    
    echo -e "${GREEN}✅ 版本 $version 已创建成功!${NC}"
    echo ""
    
    # 显示版本信息
    show_current_version
    echo ""
    
    if [ "$push" = true ]; then
        echo -e "${GREEN}🚀 推送到GitHub...${NC}"
        git push origin main
        git push origin "$version"
        echo -e "${GREEN}🎉 版本 $version 已发布!${NC}"
        echo ""
        echo "Docker镜像将会自动构建:"
        echo "  yongzz668/sqnb:$version"
    else
        echo -e "${YELLOW}📋 请手动运行以下命令发布:${NC}"
        echo "  git push origin main"
        echo "  git push origin $version"
        echo ""
        echo "或者使用以下命令自动发布:"
        echo "  $0 $version --push"
    fi
}

# 运行主函数
main "$@"
