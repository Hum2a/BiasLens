import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyCGJVoqErK2zin-VNCfVJ_cwziHH48vzs8",
    authDomain: "biaslens-2782f.firebaseapp.com",
    projectId: "biaslens-2782f",
    storageBucket: "biaslens-2782f.firebasestorage.app",
    messagingSenderId: "918274193713",
    appId: "1:918274193713:web:cd62b39ac2e6bc058c5810",
    measurementId: "G-9NZ8GRQYLK"
  };

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export default db;
