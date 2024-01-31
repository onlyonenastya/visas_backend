package models

type Request struct {
	AccessToken int64 `json:"access_token"`
	OrderId    int64 `json:"order_id"`
}
