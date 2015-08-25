## $Id$
## 定义变量，后续用 $() 方式调用变量
VERSION = 0.1
DOCBOOKXSL = ../../docbook-xsl/html/docbook.xsl
XSL-CHM = ./style-chm.xsl
XSL-HTML-SINGLEFILE = ./style-single-file.xsl
SRC = ./Road2DocBook-Beginning.xml
SRC-TEMP = temp-gb.xml
HHC = hhc.exe

## 定义处理规则，以便处理多个文件
## $@ 表示目标文件，$< 表示依赖关联文件
## 注意，前置空白对齐采用制表符（Tab键），而不是空格
%.html: %.xml
	xsltproc \
		--nonet \
		--output $@ \
		$(XSL-HTML-SINGLEFILE) \
		$<

## 定义目标操作“html”，利用上述处理规则生成指定的html文件
html:	Road2DocBook-Beginning.html

## 定义目标操作“html2”，直接指定操作内容
html2:
	xsltproc \
		--nonet \
		--output Road2DocBook-Beginning.html \
		$(XSL-HTML-SINGLEFILE) \
		$(SRC)

## 定义目标操作“chm”
chm2:
## 考虑到输出的中间文件很多，因此建立临时文件目录
	mkdir -p dist 
## html workshop 不支持 UTF-8 编码，因此将源文件转换成 GB18030 编码
	xmllint --format --encode "GB18030" --output dist/src-gb.xml $(SRC)
	xsltproc \
		--nonet \
		--output dist/* \
		$(XSL-CHM) \
		dist/src-gb.xml
## hhc 结束后，会输出错误代码，因此必须用 - 加以忽略
	-$(HHC) dist/htmlhelp.hhp
	mv -f dist/htmlhelp.chm Road2DocBook.chm

clean2:
	rm dist/*.*

chm:
## html workshop 不支持 UTF-8 编码，因此将源文件转换成 GB18030 编码
	xmllint --format --encode "GB18030" --output $(SRC-TEMP) $(SRC)
	xsltproc \
		--nonet \
		$(XSL-CHM) \
		$(SRC-TEMP)
## hhc 结束后，会输出错误代码，因此必须用 - 加以忽略
	-$(HHC) htmlhelp.hhp
	mv -f htmlhelp.chm Road2DocBook.chm

## 本节主要用于清理 html workshop 的过程文件
clean:
	rm -f *.hhc
	rm -f *.hhp
	rm -f ar*.html
	rm -f bi*.html
	rm -f ch*.html
	rm -f pr*.html
	rm -f ap*.html
	rm -f index.html
	rm -f $(SRC-TEMP)


