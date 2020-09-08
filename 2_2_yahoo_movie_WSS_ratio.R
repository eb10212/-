setwd("E:/R_data mining")
getwd()
x=read.table("movie_table.csv", header=T, sep=",",encoding = 'UTF-8')#讀取movie-類別資料集
model_data <- data.frame(x$劇情,x$犯罪,x$歷史,x$動作,x$懸疑,x$戰爭,x$冒險,x$喜劇,
                         x$恐怖,x$奇幻,x$愛情,x$音樂,x$科幻,x$溫馨,x$動畫,x$紀錄片,
                         x$勵志,x$武俠,x$影展,x$戲劇,x$影集)
WSS_ratio <- rep(NA, times = 100)                    #設定組內距離平方和變數
for (k in 1:length(WSS_ratio)) 
{
  Cluster_km <- kmeans(model_data[-1], nstart=15,centers=k,iter.max = 100)
  WSS_ratio[k] <- Cluster_km$tot.withinss
}

plot(WSS_ratio, type="b", main = "陡坡圖")
