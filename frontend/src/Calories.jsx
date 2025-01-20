import { useState, useRef } from "react"
import getCalories from "./api.js"
import Popup from "./Popup.jsx";

function Calories(){
    const inputRef = useRef(null);
    const [image, setImage] = useState(null);
    const [displayImage, setDisplay] = useState(null)
    const [popup, setPopup] = useState(false)
    const [name, setName] = useState("");
    const [cal, setCal] = useState("");
    const [pro, setPro] = useState("");

    const handleImage = (event) => {
        const file = event.target.files[0];
        setImage(file);
        if (file){
            const reader = new FileReader();
            reader.onload = () => setDisplay(reader.result);
            reader.readAsDataURL(file);
        }
    }

    const inputImage = async() => {
        const response = await getCalories(image)
        setPopup(true)
        setName(response[0])
        setCal(response[1])
        setPro(response[2])
    }

    const onInputFile = () =>{
        if (inputRef.current) {
            inputRef.current.click();
        }
    }

    const handleDelete = () =>{
        setImage(null)
    }

    const hidePopup = () => {
        setPopup(false)
    }

    return(
        <body>
            <h1>Calorie Detector</h1>
            <input type="file" accept="image/*" onChange={handleImage} style={{display: 'none'}} ref={inputRef}/>
            <button className="upload" onClick={onInputFile}>
                <span className="material-symbols-rounded">upload</span> Upload File
            </button>
            {image && <div className="selected_file">
                <p>{image.name}</p>
                <button onClick={handleDelete}>
                    <span className="material-symbols-rounded">delete</span>
                </button>
            </div>}

            {image && 
                <img src= {displayImage} alt="" />
            }
            
            <button className="submit" onClick={inputImage}>Submit</button>
            {popup && <Popup name = {name} cal = {cal} pro = {pro} onClose={hidePopup}></Popup>}
        </body>
    )
}

export default Calories