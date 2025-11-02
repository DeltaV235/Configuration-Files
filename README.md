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

## 注意事项

- 配置文件可能包含个人偏好设置，使用前请根据实际情况调整
- Clash 配置中的敏感信息（如订阅链接）会被 pre-commit hook 自动清理
- 部分脚本路径可能需要根据实际环境调整

## 许可证

个人配置文件，仅供参考。
