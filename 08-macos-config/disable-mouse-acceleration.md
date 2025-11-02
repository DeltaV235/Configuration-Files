# Disable Mouse Acceleration

在终端中输入以下指令：

```bash
defaults write .GlobalPreferences com.apple.mouse.scaling -1`
```

其中，com.apple.mouse.scaling为鼠标加速的配置名称，可以通过替换为com.apple.trackpad.scaling来关闭触控板加速，即：

```bash
defaults write .GlobalPreferences com.apple.trackpad.scaling -1`
```
回车后应该不会显示任何东西，这时重启电脑后就生效了。

如果担心是否修改成功，可以将write替换为read来查看修改后的参数：

```bash
defaults read .GlobalPreferences com.apple.mouse.scaling 
```

这种方法非常简单便捷而且高效，不用安装第三方软件，省去了下软件的功夫。如果想回到原来的状态，在设置里将鼠标跟踪速度随便设置一下就行了。
