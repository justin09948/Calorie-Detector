import styles from './Popup.module.css'

function Popup(props){
    return(
        <body className={styles.body}>
            <div className={styles.text}>
                <div>
                    <h1>Food</h1>
                    <p>{props.name}</p>
                </div>
                <div>
                    <h1>Calories</h1>
                    <p>{props.cal}g</p>
                </div>
                <div>
                    <h1>Protein</h1>
                    <p>{props.pro}g</p>
                </div>
                <button className={styles.close} onClick={props.onClose}>
                    <span className='material-symbols-rounded'>close</span>
                </button>
            </div>
        </body>
    )
}

export default Popup