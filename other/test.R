n <- 1; n.rep <- 1000000
x <- matrix(rnorm(n*n.rep), ncol=n)
print(sd(apply(x, 1, median))^2)

print(1 / (4 * (1) * dnorm(0)^2))

# library(plotly)

# x <- runif(500, min=3, max=6)
# y <- runif(500, min=3, max=6)

# fig <- plot_ly(type = 'scatter', mode = 'markers') 
# fig <- fig %>%
#   add_trace(
#     x = x,
#     y = y,
#     marker = list(
#       color = 'rgb(17, 157, 255)',
#       size = 20,
#       line = list(
#         color = 'rgb(231, 99, 250)',
#         width = 2
#       )
#     ),
#     showlegend = F
#   ) 
# fig <- fig %>%
#   add_trace(
#     x = c(2),
#     y = c(4.5),
#     marker = list(
#       color = 'rgb(17, 157, 255)',
#       size = 120,
#       line = list(
#         color = 'rgb(231, 99, 250)',
#         width = 12
#       )
#     ),
#     showlegend = F
#   )

# print(fig)