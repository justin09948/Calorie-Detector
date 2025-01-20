import axios from "axios";

async function getCalories(file){
    try{
        const data = new FormData()
        data.append("image", file)
        const response = await axios.post("http://127.0.0.1:8000/process-image/", data,{
            headers: {
                "Content-Type": "multipart/form-data",
            }
        }
        )
        return response.data
    }
    catch(error){
        console.log("error")
    }
}

export default getCalories