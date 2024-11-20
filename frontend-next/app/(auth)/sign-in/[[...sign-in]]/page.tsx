"use client";
import axios from "axios";
import Link from "next/link"
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const Page = () => {
  const Router = useRouter();

  const [user, setUser] = useState({
        password: "",
        email: ""
    })
    const [buttonDisabled, setButtonDisabled] = useState(false);
    const [loading, setLoading] = useState(false);

    const onLogin = async () => {
      try{
        setLoading(true)
        const response = await axios.post("http://127.0.0.1:5000/api/login", user);
        console.log("signup success", response.data);
        Router.push("/dashboard")
      } catch (e) {
        console.log("login failed", e)
      } finally {
        setLoading(false)
      }
    }

    useEffect(() => {
        if (user.email.length > 0 && user.password.length > 0) {
            setButtonDisabled(false)
        } else {
            setButtonDisabled(true)
        }
    }, [user])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
            <h1>{loading ? "Processing" : "Login"}</h1>
            <hr />
            <label htmlFor="email">Email</label>
            <input
                className="p-2 text-black border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-gray-600"
                type="text"
                value={user.email}
                onChange={(e) => setUser({ ...user, email: e.target.value })}
                placeholder="email"
            />
            <label htmlFor="password">Password</label>
            <input
                className="p-2 text-black border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-gray-600"
                type="password"
                value={user.password}
                onChange={(e) => setUser({ ...user, password: e.target.value })}
                placeholder="password"
            />
            <button
                onSubmit={onLogin}
                onClick={onLogin}
                className="p-2 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-gray-600">
                {buttonDisabled ? "Fill in details" : "Login"}
            </button>
            <Link href="/sign-up">
                Signup here
            </Link>
        </div>
  );
};

export default Page;
