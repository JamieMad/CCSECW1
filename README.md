# CCSECW1

Notes: Using flaskAPI stuff:
    in package.json add proxy
    Use fetch("pathname") to get data and useEffect


    Example :
    const [data, setData] = useState([{}])
    useEffect(() => {
        fetch("/hello").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }   
        )
    }, [])


# Set Up
    Go to root directory
    flask --app api run
    Go to ./react/api
    npm start
