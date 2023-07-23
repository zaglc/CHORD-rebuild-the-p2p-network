# CHORD-rebuild-the-p2p-network
it's a project in network of computer and was implemented directly and simply (without Concurrent Operations), also the first pr in github for me, any comments are welcomed

## 功能实现

+ chord网络基本结构
+ 统计查询的跳数分布：experiment.py文件中average分支，产生概率分布曲线pdf.png

<img src=https://github.com/zaglc/CHORD-rebuild-the-p2p-network/blob/main/figs/pdf.png width = "450" height = "300" alt="图片名称" align=center>

+ 统计不同服务器节点数目下跳数的统计特征：experiment.py中multihop分支，1、99分位数和均值，产生box.png

<img src=https://github.com/zaglc/CHORD-rebuild-the-p2p-network/blob/main/figs/box.png width = "450" height = "300" alt="图片名称" align=center>

+ 比较优化前后平均查询数目变化：experiment.py中modest分支，其中优化非常简单，就是若待查询位置落在节点的predecessor和节点之间，就直接返回不需查询；motivation：这样的查询是次数可能会最多的，且最容易降低的

<img src=https://github.com/zaglc/CHORD-rebuild-the-p2p-network/blob/main/figs/last.png width = "450" height = "300" alt="图片名称" align=center>

+ 生成查询gif动图：需要预先准备简单脚本，如script目录下的文件；其中每次lookup操作都会生成一份gif，储存在visualize中，若哈希环大小和查询目标id相同，会覆盖，代码实现于demo.py
+ 可以模拟chord节点加入删除，数据存储移除的过程，实现于simulate.py

## 代码说明

+ 由于实现问题，运行前需要修改`utils.py`中的`IL_LEN`变量，哈希环大小为$2^{IL\_LEN}$
+ 未使用parser包，参数输入顺序和数量固定
+ 运行实验：将`IL_LEN`改为30，给入合适参数并在code下运行
  + average分支中，参数12代表哈希环上点数为$2^{12}$
  + multihop分支中，0和1代表不适用优化和使用优化，2、8代表8组实验，点数从$2^{2}$逐渐增加至$2^{2+8}$
  + modify分支需要先用优化和不优化的参数运行multihop分支，生成data-npy文件后才可运行

  ```
  python experiment.py average 12
  python experiment.py multihop 0 2 8
  python experiment.py multihop 1 2 8
  python experiment.py modify
  ```
+ 生成可视化：将`IL_LEN`改为3，4或5，直接运行

  <img src=https://github.com/zaglc/CHORD-rebuild-the-p2p-network/blob/main/visualize/5_lookup_30/total.gif width = "450" height = "450" alt="图片名称" align=center>
  
  ```
  python demo.py <path>
  ```
  path为两个script的地址，script2最好用5来运行，不然可能冲突 
+ 自定义网络：将`IL_LEN`改为30，运行
  ```
  python simulate.py
  ```
  交互式界面中可输入如下命令：
  + join `str`：增加服务器节点
  + leave `str`：移除服务器节点
  + lookup `str`：查找str对应的key，若str正好也对应服务器，会显示服务器信息
  + insert `key` `value`：增加键值对
  + delete `key`：删除键值对
  + show：展示所有服务器信息
  + clear：删除所有服务器
  + q：退出
  
  如果发生冲突或者节点不存在，会给warning，不会报错
