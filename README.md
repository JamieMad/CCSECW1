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

    For some reason it does 2 requests


# Set Up
    flask --app api db init
    flask --app api run


TODO:
    Maybe make a class for API requests etc, e.g. call Rest.register(registrationData)