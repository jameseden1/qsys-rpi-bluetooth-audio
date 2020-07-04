-----
-- Setup socket
-----

address = '10.42.62.185'
port = 10000
sock = TcpSocket.New()
sock.ReadTimeout = 0
sock.WriteTimeout = 0
sock.ReconnectTimeout = 5
enabled = false

sock.Connected = function(sock)
  print('TCP socket is connected')
  sock:Write('status:enable')
end

sock.Reconnect = function(sock)
  print('TCP socket is reconnecting')
  Controls.Outputs[1].String = 'Status: Reconnecting'
end

sock.Closed = function(sock)
  print('TCP socket was closed by the remote end')
  Controls.Outputs[1].String = 'Status: Closed'
end

sock.Error = function(sock, err)
  print('TCP socket had an error:',err)
  Controls.Outputs[1].String = 'Status: Error connecting'
end

sock.Timeout = function(sock, err)
  print('TCP socket timed out',err)
  Controls.Outputs[1].String = 'Status: Timed Out'
end

sock.Data = function(sock)
  status = sock:Read(sock.BufferLength)
  Controls.Outputs[1].String = status
end

function run()
  Controls.Outputs[1].String = 'Status: Establishing Connection'

  sock:Connect(address, port)

  btn_disconnect = Controls.Inputs[1];
  btn_disconnect.EventHandler=function(btn)
   sock:Write('disconnect')
  end

  btn_restart = Controls.Inputs[2];
  btn_restart.EventHandler=function(btn)
   sock:Write('restart')
  end

  btn_reboot = Controls.Inputs[3];
  btn_reboot.EventHandler=function(btn)
   sock:Write('reboot')
  end

  btn_enable = Controls.Inputs[4];
  btn_enable.EventHandler=function(btn)
    if btn.Value == 1 then
      enabled = true
    else
      enabled = false
    end
  end
  
  -- read the initial value from enabled/disabled before we send the first command
  if btn_enable.Value == 1 then
    enabled = true
  else
    enabled = false
  end

  function timerFunc()
    if enabled == true then
      sock:Write('status:enable')
    else
      sock:Write('status:disable')
    end

    Timer1:Start(1)
  end

  Timer1 = Timer.New()
  Timer1.EventHandler = timerFunc
  Timer1:Start(1)
end

run()
