#docker web
------------------------

一个小的网站模型，单页面，功能是显示B站上特定用户关注了哪些用户。

前端用的是bootstrap + D3.js绘制关注图，后端用的是tornado + MongoDB，同时用requests抓取用户数据，用pyinstaller把python脚本打包成静态可执行文件。

最后用docker打包了一下。

找个装有Docker toolbox的环境，执行下下面两句就能看到效果，如果docker镜像拖不下来的话记得准备梯子。
> docker-compose build
> docker-compose up -d
然后浏览器访问docker环境的80端口就行。


基本上就是个无聊时练手的作品，没什么卵用。


> Written with [StackEdit](https://stackedit.io/).