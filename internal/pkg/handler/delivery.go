package handler

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"lab8/internal/models"
	"math/rand"
	"net/http"
	"time"
)


func (h *Handler) issueDeliveryDate(c *gin.Context) {
	var input models.Request
	if err := c.BindJSON(&input); err != nil {
		newErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}
	fmt.Println("handler.issueDeliveryDate:", input)

	c.Status(http.StatusOK)


	go func() {
		time.Sleep(3 * time.Second)
		sendDeliveryDateRequest(input)
	}()
}

func sendDeliveryDateRequest(request models.Request) {

	var deliveryDate = "Наруения отсутствуют"
	
	if rand.Intn(2) == 1 {
		deliveryDate = "Есть нарушения"
	}
	fmt.Println(deliveryDate)
	answer := models.DeliveryDateRequest{
		AccessToken: request.AccessToken,
		DeliveryDate: deliveryDate,
	}

	client := &http.Client{}

	jsonAnswer, _ := json.Marshal(answer)
	bodyReader := bytes.NewReader(jsonAnswer)

	requestURL := fmt.Sprintf("http://127.0.0.1:8000/api/orders/%d/update_delivery_date/", request.OrderId)

	req, _ := http.NewRequest(http.MethodPut, requestURL, bodyReader)

	req.Header.Set("Content-Type", "application/json")

	response, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending PUT request:", err)
		return
	}

	defer response.Body.Close()

	fmt.Println("PUT Request Status:", response.Status)
}
