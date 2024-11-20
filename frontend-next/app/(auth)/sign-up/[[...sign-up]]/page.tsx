"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

const Page = () => {
  const router = useRouter();

  const [user, setUser] = useState({
    email: "",
    password: "",
    username: "",
  });
  const [buttonDisabled, setButtonDisabled] = useState(false);
  const [loading, setLoading] = useState(false);

  const onSignup = async () => {
    try {
      setLoading(true);
      console.log("signup", user);
      const response = await axios.post("http://127.0.0.1:5000/api/register", user);
      console.log("signup success", response.data);
      router.push("/sign-in");
    } catch (e) {
      console.log("signup failed", e);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    if (
      user.email.length > 0 &&
      user.password.length > 0 &&
      user.username.length > 0
    ) {
      setButtonDisabled(false);
    } else {
      setButtonDisabled(true);
    }
  }, [user]);

  return (
    <div className="mt-20 flex flex-col items-center justify-center min-h-screen py-2">
      <h1>{loading ? "processing" : "Signup"}</h1>
      <hr />
      <label htmlFor="username">username</label>
      <input
        className="p-2 text-black border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-gray-600"
        type="text"
        value={user.username}
        onChange={(e) => setUser({ ...user, username: e.target.value })}
        placeholder="username"
      />
      <label htmlFor="email">email</label>
      <input
        className="p-2 text-black border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-gray-600"
        type="text"
        value={user.email}
        onChange={(e) => setUser({ ...user, email: e.target.value })}
        placeholder="email"
      />
      <label htmlFor="password">password</label>
      <input
        className="p-2 text-black border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-gray-600"
        type="password"
        value={user.password}
        onChange={(e) => setUser({ ...user, password: e.target.value })}
        placeholder="password"
      />
      <button
        onSubmit={onSignup}
        onClick={onSignup}
        className="p-2 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-gray-600"
      >
        {buttonDisabled ? "Fill in details" : "Signup"}
      </button>
      <Link href="/sign-in">Already a user? Login here</Link>
    </div>
  );
};

export default Page;
