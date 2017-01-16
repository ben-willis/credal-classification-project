######### Useful Fns ##############
# Discretize continuous data into n bins
discretize <- function(data, n) {
  as.numeric(cut(data, breaks=quantile(data, probs=seq(0,1,length.out=n), na.rm=TRUE)))
}

# Split a data frame into n equally sized dataframes
split_data_frame <- function(df, n) {
  split(df, rep(1:n, length.out=nrow(df)))
}

######### Probabilities ##########
# P(C)
p.class <- function(df, classColumn) {
  counts = table(df[classColumn])
  probabilities = counts / sum(counts)
  return(probabilities)
}

# P(A_i | C)
p.feature_given_class <- function(df, featureColumn, classColumn) {
  counts = table(df[c(featureColumn, classColumn)])
  probabilities = counts / apply(counts, 1, sum)
  return(probabilities)
}

########### Cross Validation ##############
# Classify an opject and compare against actual class
cv.validate <- function(train_df, test_df) {
  success <- apply(test_df, 1, function(object) {
    best_guess = classifier.mle(train_df)
    return(best_guess(object) == object["Symboling"])
  })
  
  return(length(which(success==TRUE))/length(success))
}

# Split the data frame then validate each sub-frame
cv.cross_validate <- function(df) {
  split_df <- split_data_frame(df, 10)
  success <- sapply(1:length(split_df), function(test_df_id) {
    test_df <- split_df[[test_df_id]]
    train_df <- do.call("rbind", split_df[-test_df_id])
    return(cv.validate(train_df, test_df))
  })
  return(mean(success))
}

############ Classifier ##################
# Maximum Likelihood Estimate for class
classifier.mle <- function(train_df) {
  symbols = c("-2","-1","0","1","2","3")
  
  nbc.p.body_style_given_class = p.feature_given_class(train_df, "Body.style", "Symboling")
  nbc.p.price_given_class = p.feature_given_class(train_df, "Price", "Symboling")
  nbc.p.length_given_class = p.feature_given_class(train_df, "Length", "Symboling")
  
  best_guess <- function(object) {
    # P(A|C) = P(A_1|C) * ... * P(A_k|C)
    likelihoods = sapply(symbols, function(symbol) {
      prod(c(
        nbc.p.length_given_class[object["Length"], symbol],
        nbc.p.body_style_given_class[object["Body.style"], symbol],
        nbc.p.price_given_class[object["Price"], symbol]
      ))
    })
    
    return(names(which.max(likelihoods)))
  }
  return(best_guess)
}

############### Use on data ##################
# Load data
df <- read.table('../data/automobile.csv', header=TRUE, sep=",")
df <- df[,c('Price', 'Length', 'Body.style', 'Symboling')]

# Discretize and convert to integers
df$Length <- discretize(df$Length, 10)
df$Price <- discretize(df$Price, 10)
df$Body.style <- as.numeric(df$Body.style)

print(cv.cross_validate(df))