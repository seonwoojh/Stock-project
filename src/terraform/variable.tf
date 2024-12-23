variable "region" {
  type        = string
  description = "aws 리전"
  default     = "ap-northeast-2"
}

variable "access_key" {
  type        = string
  description = "Enter access_key"
  default     = ""
}

variable "secret_key" {
  type        = string
  description = "Enter secret_key"
  default     = ""
}

variable "admin_cidr_blocks" {
  type    = list(string)
  default = ["182.xxx.xxx.x/32"]
}