import { useCallback, useEffect, useState } from "react";
import { GameScreen } from "./screens/GameScreen";
import "./styles/flexStyles.css";

import playBtn from "./assets/play.png";

import blackjackLogo from "./assets/blackjack.png";
import coinArea from "./assets/coinArea.png";
import rulesBtn from "./assets/rules.png";
import rule1 from "./assets/rule1.png";
import rule2 from "./assets/rule2.png";
import rule3 from "./assets/rule3.png";
import rule4 from "./assets/rule4.png";

import loginBtn from "./assets/login.png";
import signupBtn from "./assets/signup.png";

import { useCoinValue } from "./hooks/useCoinValue";

import { currencyFormatter } from "../../../utils/index";
import { Modal } from "antd";
import { Tabs } from "antd";
import type { TabsProps } from "antd";

import { Input, notification } from "antd";

const AUTHORIZATION_KEY = "auth_key";

const items: TabsProps["items"] = [
  {
    key: "1",
    label: "Game Rules",
    children: <img src={rule1} style={{ width: "100%" }} />,
  },
  {
    key: "2",
    label: "Game Actions",
    children: <img src={rule2} style={{ width: "100%" }} />,
  },
  {
    key: "3",
    label: "Card Values",
    children: <img src={rule3} style={{ width: "100%" }} />,
  },
  {
    key: "4",
    label: "Gameplay Information",
    children: <img src={rule4} style={{ width: "100%" }} />,
  },
];

function App() {
  const [start, setStart] = useState(false);
  const location = window.location;
  const [history, setHistory] = useState([]);
  const [localStorageCoins, setLocalStorageCoins] = useCoinValue(100000);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [authorized, setAuthorized] = useState(() => {
    const data = window.localStorage.getItem(AUTHORIZATION_KEY);
    if (data) {
      try {
        const parsedData = JSON.parse(data);
        return true;
      } catch {
        return false;
      }
    }
    return false;
  });
  const [isLoginMode, setIsLoginMode] = useState(true);

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  async function getHistory() {
    const res = await fetch("http://localhost:8000/getHistory", {
      method: "GET",
      headers: {
        "Access-Control-Allow-Origin": "http://localhost:8000",
        "Content-Type": "application/json",
      },
    });
    const jsoned = await res.json();
    setHistory(jsoned);
    console.log("history", jsoned);
  }

  const resetBalance = useCallback(() => {
    const now = new Date();
    const night = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate() + 1,
      0,
      0,
      0
    );
    const msToMidnight = night.getTime() - now.getTime();
    setTimeout(() => {
      setLocalStorageCoins(100000);
      resetBalance();
    }, msToMidnight);
  }, [setLocalStorageCoins]);

  useEffect(() => {
    resetBalance();
  }, [resetBalance]);

  useEffect(() => {
    getHistory();
  }, []);

  useEffect(() => {
    const authVal = localStorage.getItem("auth");
    let auth = null;
    try {
      auth = JSON.parse(authVal ? authVal : "no");
    } catch {
      auth = "no";
    }

    if (auth === "yes") {
      setAuthorized(true);
    }
  }, []);

  async function login() {
    if (!password || !username) {
      notification.open({
        type: "error",
        message: "Please fill the empty fields.",
      });
      return;
    }
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        // "Access-Control-Allow-Origin": "http://localhost:8001",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ password: password, username: username }),
    });
    const jsoned = await res.json();
    if (jsoned.res === -1) {
      notification.open({
        type: "error",
        message: "No such account exist.Please signup first.",
      });
    } else if (jsoned.res === -2) {
      notification.open({
        type: "error",
        message: "Username or password incorrect.",
      });
    } else {
      window.localStorage.setItem(AUTHORIZATION_KEY, "true");
      setAuthorized(true);
    }
  }

  async function signup() {
    const res = await fetch("http://localhost:8000/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        username: username,
        password: password,
      }),
    });
    const jsoned = await res.json();
    if (jsoned.res === "success") {
      notification.open({
        type: "success",
        message: "Account created successfull.Use the credentials to login.",
      });
    }
    setIsLoginMode(true);
    console.log("Jsoned is", jsoned);
  }

  if (location.toString().includes("gamehistory")) {
    return (
      <div>
        {history.map((h) => (
          <div>
            <div>{h}</div>
            <br />
          </div>
        ))}
      </div>
    );
  }

  if (start) {
    return (
      <div className="gameBoard">
        <img
          src={blackjackLogo}
          style={{
            position: "absolute",
            left: 20,
            top: 20,
            height: "66px",
            width: "322px",
          }}
        />
        <div style={{ position: "absolute", right: 100, top: 20 }}>
          <img src={coinArea} height={86} width={368} />

          <span
            style={{
              position: "absolute",
              right: 0,
              zIndex: 1,
              top: 30,
              color: "white",
              fontSize: "25px",
              width: "110%",
              textAlign: "center",
            }}
          >
            {currencyFormatter(localStorageCoins)}
          </span>

          <span
            style={{
              position: "absolute",
              right: 125,
              top: 75,
              fontSize: "20px",
              color: "white",
            }}
          >
            coin will reset every 24h
          </span>
        </div>

        <div className="screen">
          <GameScreen
            localStorageCoins={localStorageCoins}
            setLocalStorageCoins={setLocalStorageCoins}
          />
        </div>
      </div>
    );
  }

  if (!authorized) {
    return (
      <div className="authScreen">
        <div
          style={{
            height: "600px",
            width: "700px",
            marginLeft: "auto",
            marginRight: "auto",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            background: "#00000080",
            borderRadius: "15px",
            padding: "48px",
            gap: "30px",
          }}
        >
          <img
            src={blackjackLogo}
            style={{ height: "115px", width: "564px" }}
          />
          <div style={{ textAlign: "center" }}>
            <p style={{ fontSize: 40, color: "white" }}>
              {isLoginMode ? "Log in " : "Sign up"}
            </p>
            <p style={{ fontSize: 40, color: "white" }}>to play the game</p>
          </div>
          <div
            style={{ display: "flex", flexDirection: "column", gap: "40px" }}
          >
            {!isLoginMode && (
              <Input
                placeholder="email"
                style={{ height: "50px", width: "400px" }}
                onChange={(e) => setEmail(e.target.value)}
                value={email}
              />
            )}
            <Input
              placeholder="username"
              style={{ height: "50px", width: "400px" }}
              onChange={(e) => setUsername(e.target.value)}
              value={username}
            />
            <Input.Password
              placeholder="password"
              style={{ height: "50px", width: "400px" }}
              onChange={(e) => setPassword(e.target.value)}
              value={password}
            />
          </div>
          {isLoginMode ? (
            <div>
              <img
                src={signupBtn}
                style={{ marginRight: "20px", cursor: "pointer" }}
                onClick={() => setIsLoginMode(false)}
              />
              <img
                src={loginBtn}
                style={{ cursor: "pointer" }}
                onClick={() => login()}
              />
            </div>
          ) : (
            <div>
              <img
                src={loginBtn}
                style={{ marginRight: "20px", cursor: "pointer" }}
                onClick={() => setIsLoginMode(true)}
              />
              <img
                src={signupBtn}
                style={{ cursor: "pointer" }}
                onClick={() => signup()}
              />
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="introScreen">
      <div style={{ position: "absolute", bottom: 50 }}>
        <img
          src={playBtn}
          onClick={() => setStart(true)}
          style={{
            width: "194px",
            height: "80px",
            cursor: "pointer",
          }}
        />
        <img
          src={rulesBtn}
          onClick={showModal}
          style={{
            width: "194px",
            height: "80px",
            marginLeft: "20px",
            cursor: "pointer",
          }}
        />
      </div>
      <Modal
        title="How to play?"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleOk}
        footer={null}
        width={"80%"}
        centered
      >
        <Tabs
          defaultActiveKey="1"
          items={items}
          onChange={(key: string) => console.log(key)}
        />
      </Modal>
    </div>
  );
}

export default App;
