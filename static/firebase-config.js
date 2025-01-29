// firebase-config.js

// Import Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.16.0/firebase-app.js";
import { 
    getAuth, 
    signInWithEmailAndPassword, 
    signOut, 
    onAuthStateChanged 
} from "https://www.gstatic.com/firebasejs/9.16.0/firebase-auth.js";
import { 
    getFirestore 
} from "https://www.gstatic.com/firebasejs/9.16.0/firebase-firestore.js";
import { 
    getDatabase, 
    ref, 
    onValue, 
    set, 
    update 
} from "https://www.gstatic.com/firebasejs/9.16.0/firebase-database.js";

// Firebase Configuration
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
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const realtimeDB = getDatabase(app);

// Export Firebase Authentication
export { app, auth, signInWithEmailAndPassword, signOut, onAuthStateChanged };

// Export Firestore
export { db };

// Export Firebase Realtime Database Functions
export { realtimeDB, ref, onValue, set, update };
