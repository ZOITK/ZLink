// Package config - 범용 설정 로더
package config

import (
	"os"
	"strconv"
)

// Config - 서버 기본 설정 구조체
type Config struct {
	NodeEnv             string
	TCPPort             int
	UDPPort             int
	UseMapSectorFilter  bool
}

// Load - 환경 변수로부터 설정을 로드합니다.
func Load() *Config {
	return &Config{
		NodeEnv:            getEnv("NODE_ENV", "development"),
		TCPPort:            getEnvAsInt("TCP_PORT", 8080),
		UDPPort:            getEnvAsInt("UDP_PORT", 8081),
		UseMapSectorFilter: getEnvAsBool("USE_MAP_SECTOR_FILTER", false),
	}
}

func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}

func getEnvAsInt(key string, defaultValue int) int {
	valueStr := getEnv(key, "")
	if value, err := strconv.Atoi(valueStr); err == nil {
		return value
	}
	return defaultValue
}

func getEnvAsBool(key string, defaultValue bool) bool {
	valueStr := getEnv(key, "")
	if value, err := strconv.ParseBool(valueStr); err == nil {
		return value
	}
	return defaultValue
}
