library(limma)
library(optparse)

# make options
option_list <- list( 
    make_option(c("-s", "--sample_list"), action="store"),
    make_option(c("-r", "--result_dir"), action="store"),
    make_option(c("-o", "--limma_result"), action="store"),
    make_option(c("-l", "--sample_num_list"), action="store"),
    make_option(c("-c", "--count_table"), action="store")
    )

opt <- parse_args(OptionParser(option_list=option_list))

result_dir <- opt$result_dir
sample_list <- unlist(strsplit(opt$sample_list, ";"))
sample_num_list <- unlist(strsplit(opt$sample_num_list, ";"))
count_table_file <- opt$count_table
final_result_file <- opt$limma_result

output_prefix <- paste(unique(sample_num_list), collapse="_")

print("**** arguments ****")
result_dir
sample_list
count_table_file
final_result_file
sample_num_list
output_prefix
print("**** arguments ****")

# read couting table
#mycounts <- read.table(count_table_file, header=TRUE, row.names=1)
print("asdfasdfasdadf")
print(count_table_file)
mycounts <- read.table(count_table_file, header=FALSE, row.names=1, sep = "\t", comment.char="")
print(head(mycounts))
mat <- as.matrix(mycounts) 

# remove class labels
#mat <-(mat[-1,])
print(head(mat))
# log2 transform to fit limma input
mat <-log2(mat)

# remove Inf values
mat <- mat[!apply(mat, 1, function(x) {any(x == -Inf)}),]

# add 'p' to call class name since '1' is not proper class name
#Group <- factor(paste("p", sample_num_list, sep=""))
Group <- factor(sample_num_list)
print(Group)
design <- model.matrix(~0 + Group)
colnames(design) <- gsub("Group","", colnames(design))
fit <- lmFit(mat,design)
colnames(design)[1]
colnames(design)[2]

temp <- paste(colnames(design)[2],colnames(design)[1],sep="-")
print("adsfadsf")
print(temp)

contrast.matrix<-makeContrasts(temp,levels=design)
fit2<-contrasts.fit(fit,contrast.matrix)
fit2<-eBayes(fit2)

#raw counts 
#result_fig <- paste(result_dir, "/",output_prefix,"_heatmap1.jpg", collapse = "", sep="") 
#jpeg(result_fig)
#heatmap.2(counts(fit2,normalized=TRUE)[select,], col = hmcol, Rowv = FALSE, Colv = FALSE, scale="none", dendrogram="none", trace="none", margin=c(10,8), cexCol=1)
#dev.off()
# volcano plot
#result_fig <- paste(result_dir, "/",output_prefix,"_heatmap1.jpg", collapse = "", sep="") 
#result_fig
#jpeg(result_fig)
#volcanoplot(fit2,coef=2)
#dev.off()


cat("[INFO] decideTests\n")
results <- decideTests(fit2)
head(results)

cat("[INFO] Store result to files\n")
limma_result1=topTable(fit2, n=Inf, coef=1, adjust="BH")

#write.table(limma_result1, file=paste(result_dir,"/limma_result1.txt", sep=""), row.names =TRUE, col.names = TRUE, sep ="\t", quote=FALSE)
write.table(limma_result1, file=final_result_file, row.names =TRUE, col.names = TRUE, sep ="\t", quote=FALSE)

# print out results
cat("[INFO] Store result2 to files\n")
limma_result2=topTableF(fit2, n=Inf, paste(result_dir,"/limma_result2.txt"))
write.table(limma_result2, file=paste(result_dir,"/limma_result2.txt", sep=""), row.names =TRUE, col.names = TRUE, sep ="\t", quote=FALSE)

#deg<-mat1[,1:4][sel.diif,]

