package models

type DeliveryDateRequest struct {
	AccessToken int64  `json:"access_token"`
	DeliveryDate string `json:"violation"`
}
