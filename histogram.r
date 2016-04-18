#!/usr/bin/env Rscript
library(stringr) #seriously?
args=commandArgs(trailingOnly=T)
filename=args[1]
t=paste(scan(filename, what="character"), collapse="")
p=str_locate(pattern="\\.", t) #beware, don't use a char here
t=as.integer(strsplit(substr(t, p+1, nchar(t)), split="")[[1]])
#hist(t)

library(ggplot2)
data=data.frame(digit=numeric(length(t)))
data$digit=t
title=paste("Digits repartition in ", filename)
ggplot(data, aes(digit)) +
	geom_histogram(binwidth=1, color="black", fill="NA") + xlim(0, 10) +
	labs(x="Digit", y="Count") + ggtitle(title)
