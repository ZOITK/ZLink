// Package logger - 범용 로거 라이브러리 (slog 기반)
package logger

import (
	"log/slog"
	"os"
)

// Init - 로거 초기화
func Init(env string) {
	var handler slog.Handler

	if env == "production" {
		// 운영 환경: JSON 포맷
		handler = slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
			Level: slog.LevelInfo,
		})
	} else {
		// 개발 환경: 텍스트 포맷 (색상 및 가독성 강조)
		handler = slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
			Level: slog.LevelDebug,
		})
	}

	logger := slog.New(handler)
	slog.SetDefault(logger)
}
