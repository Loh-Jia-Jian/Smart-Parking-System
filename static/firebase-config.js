// firebase-config.js
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.16.0/firebase-firestore.js";
// Import the Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.16.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/9.16.0/firebase-auth.js";
import { doc, getDoc } from "https://www.gstatic.com/firebasejs/9.16.0/firebase-firestore.js";

// Your Firebase configuration
const firebaseConfig = {
    apiKey: "apikey",
    authDomain: "authdomain",
    projectId: "project-id",
    storageBucket: "storagebucket",
    messagingSenderId: "sender-id",
    appId: "app-id",
    measurementId: "measurement-id"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
