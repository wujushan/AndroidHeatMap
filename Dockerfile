FROM golang:latest

WORKDIR $GOPATH/src/go-gin-demo

COPY . $GOPATH/src/go-gin-demo

RUN go get github.com/gin-gonic/gin && go build .

EXPOSE 8081

ENTRYPOINT ["./go-gin-demo"]
