function Card({

    children

}) {

    return (

        <div

            style={{

                background: "#1e293b",

                borderRadius: 12,

                padding: 20,

                border: "1px solid #334155",

                marginBottom: 20

            }}

        >

            {children}

        </div>

    );

}

export default Card;