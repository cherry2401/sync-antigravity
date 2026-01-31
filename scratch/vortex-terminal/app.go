package main

import (
	"context"
	"io"
	"sync"
	"vortex-terminal/internal/pty"
	"vortex-terminal/internal/ssh"

	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx          context.Context
	sessions     map[string]interface{} // Store pty.Session or ssh.Session
	sessionsLock sync.RWMutex
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{
		sessions: make(map[string]interface{}),
	}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

// CreateLocalSession spawns a new local terminal
func (a *App) CreateLocalSession(shell string, rows, cols int) string {
	s, err := pty.NewLocalSession(shell, rows, cols)
	if err != nil {
		return ""
	}

	a.sessionsLock.Lock()
	a.sessions[s.ID] = s
	a.sessionsLock.Unlock()

	// Start reader loop
	go a.readLoop(s.ID, s.Stdout)

	return s.ID
}

// CreateSSHSession connects to a remote server
func (a *App) CreateSSHSession(host, user, password string, port, rows, cols int) string {
	s, err := ssh.Connect(host, user, password, port, rows, cols)
	if err != nil {
		return ""
	}

	a.sessionsLock.Lock()
	a.sessions[s.ID] = s
	a.sessionsLock.Unlock()

	// Start reader loop
	go a.readLoop(s.ID, s.Stdout)

	return s.ID
}

func (a *App) readLoop(id string, reader io.Reader) {
	buf := make([]byte, 1024*32)
	for {
		n, err := reader.Read(buf)
		if n > 0 {
			// Emit data to frontend
			runtime.EventsEmit(a.ctx, "pty-output:"+id, string(buf[:n]))
		}
		if err != nil {
			// Session closed
			a.CloseSession(id)
			runtime.EventsEmit(a.ctx, "session-closed:"+id, nil)
			break
		}
	}
}

// WriteToSession sends input to a session
func (a *App) WriteToSession(id string, data string) {
	a.sessionsLock.RLock()
	s, ok := a.sessions[id]
	a.sessionsLock.RUnlock()

	if !ok {
		return
	}

	switch sess := s.(type) {
	case *pty.Session:
		sess.Write([]byte(data))
	case *ssh.Session:
		sess.Write([]byte(data))
	}
}

// ResizeSession resizes a session
func (a *App) ResizeSession(id string, rows, cols int) {
	a.sessionsLock.RLock()
	s, ok := a.sessions[id]
	a.sessionsLock.RUnlock()

	if !ok {
		return
	}

	switch sess := s.(type) {
	case *pty.Session:
		sess.Resize(rows, cols)
	case *ssh.Session:
		sess.Resize(rows, cols)
	}
}

// CloseSession closes a session
func (a *App) CloseSession(id string) {
	a.sessionsLock.Lock()
	s, ok := a.sessions[id]
	if ok {
		delete(a.sessions, id)
	}
	a.sessionsLock.Unlock()

	if !ok {
		return
	}

	switch sess := s.(type) {
	case *pty.Session:
		sess.Close()
	case *ssh.Session:
		sess.Close()
	}
}
