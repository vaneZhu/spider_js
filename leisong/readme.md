### 运行方式
* python LeiSong.py
#### 思路

> 大约一周之前，看到爬虫群里有一道面试题，赵雷的歌都讲的什么？
> 很多群友在diss面试官，但是我尝试着做了这道题，有一些不同的收获，于是写出来分享给大家。
> 整体思路是抓取网易云关于赵雷的所有歌词，统计词频，最后显示出来
##### 阅读流程
 * 效果展示
 * 项目地址
 * 遇到的问题
 * 总结
#### 效果展示
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190810232148486.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTMzNTYyNTQ=,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190810232047465.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTMzNTYyNTQ=,size_16,color_FFFFFF,t_70)

#### 项目地址
*  [赵雷的歌](https://github.com/justcodedroid/spider_js/tree/master/leisong)
#### 遇到的问题
* 网易云反爬
	* 网易云的反爬类似快手的反爬，都是对参数进行两次aes加密，然后在对随机数进行rsa加密。	 	
	* 	js逆向的过程是一个套路
		* 找到lyric地址，进行debug
		* 查看调用栈，找到加密参数
		* 不断debug，找到入参（原始参数），加密函数
		* 重写
* jieba分词效果
	* 需要不断的尝试，找出合适的自定义词典，然后才能更好的进行分词。 	
#### 总结

> 这里我想说的更多的是思考方式，面试官问的问题，他为什么这样问，他为什么这样思考，他想通过这个问题考察我们哪些能力？
> 相比于直接骂面试官sb，倒不如改变下我们的思考方式，认知方式。
> [认知三部曲](https://zhuanlan.zhihu.com/p/26902955)
