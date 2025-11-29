# Configuration Files

个人开发环境配置文件集合，包含各种工具和平台的配置。

## 目录结构

- **01-git-config/** - Git 配置文件
  - `gitconfig` - Git 全局配置
  - `gitmessage` - Git 提交消息模板

- **02-idea-config/** - IntelliJ IDEA 配置
  - `ideavimrc` - IdeaVim 插件配置
  - `IDEA-config-export/` - IDEA 设置导出文件
  - `sync-ideavimrc.sh` - 同步 ideavimrc 脚本

- **03-mycli-config/** - MyCLI (MySQL CLI) 配置
  - `my.cnf` - MySQL 配置文件
  - `myclirc` - MyCLI 配置文件

- **04-raspberry-config/** - 树莓派配置
  - `systemd/frpc.service` - FRP 客户端 systemd 服务配置

- **05-windows-config/** - Windows 系统配置
  - `Convert-C-h-to-BackSpace.ahk` - AutoHotkey 脚本
  - `key-layout/` - 键盘布局配置

- **06-windows-terminal-setting/** - Windows Terminal 配置
  - `settings.json` - Windows Terminal 设置
  - `windows-terminal-icon/` - 终端图标资源

- **07-wsl-config/** - WSL (Windows Subsystem for Linux) 配置
  - `vimrc` - Vim 配置
  - `zshrc` - Zsh 配置
  - `scripts/rm.sh` - 自定义脚本

- **08-macos-config/** - macOS 系统配置
  - `git/` - Git 配置文件
  - `karabiner/` - Karabiner-Elements 键盘映射配置
  - `starship/` - Starship 终端提示符配置
  - `vim/` - Vim 配置
  - `zsh/` - Zsh 配置
  - `convert-video-to-gif-by-ffmepg.sh` - 视频转 GIF 脚本
  - `disable-mouse-acceleration.md` - 禁用鼠标加速指南

- **09-clash/** - Clash 代理配置
  - `mihomo-custom.yaml` - Mihomo 自定义配置
  - `qichiyuhub-mihomo-config.yaml` - QiChiyuHub 配置
  - `tools/` - 配置管理工具

- **10-ghostty/** - Ghostty 终端模拟器配置
  - `config` - Ghostty 配置文件

- **11-rime/** - Rime 输入法配置
  - `squirrel-mac/` - macOS 鼠鬚管（Squirrel）配置
    - `*.custom.yaml` - 自定义配置文件（仅追踪这些文件）
    - 万象拼音输入方案配置
    - 自定义主题（微信亮色/暗色）
    - 键盘映射和布局设置

## Git Hooks

项目使用自定义 Git Hooks 来确保配置文件的质量：

- `.githooks/pre-commit` - 提交前自动清理 Clash 配置文件中的敏感信息

使用以下命令启用 Git Hooks：

```bash
git config core.hooksPath .githooks
```

## 使用说明

1. 克隆仓库到本地
2. 根据需要复制对应的配置文件到系统配置目录
3. 部分配置文件包含同步脚本，可直接运行脚本进行同步

### Rime 输入法配置使用

对于 Rime 配置（11-rime 目录）：

1. **macOS (鼠鬚管/Squirrel)**:
   ```bash
   # 复制 custom.yaml 文件到 Rime 用户目录
   cp 11-rime/squirrel-mac/*.custom.yaml ~/Library/Rime/

   # 部署 Rime 配置
   # 方法1: 在输入法菜单中选择 "重新部署"
   # 方法2: 使用命令行
   "/Library/Input Methods/Squirrel.app/Contents/MacOS/Squirrel" --reload
   ```

2. **配置说明**:
   - 仅追踪 `*.custom.yaml` 文件，其他生成文件和词库文件不纳入版本控制
   - 包含万象拼音输入方案和自定义主题配置
   - 修改配置后需要重新部署才能生效

## 注意事项

- 配置文件可能包含个人偏好设置，使用前请根据实际情况调整
- Clash 配置中的敏感信息（如订阅链接）会被 pre-commit hook 自动清理
- 部分脚本路径可能需要根据实际环境调整

## 许可证

个人配置文件，仅供参考。
