variable "region" {
    default = "eu-west-1"
}

variable "runtime" {
    default = "python3.8"
}

variable "start_schedule" {
    default = "cron(0 6 * * ? *)"
}

variable "stop_schedule" {
    default = "cron(0 21 * * ? *)"
}
