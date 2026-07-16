function Input({

    placeholder,

    value,

    onChange,

    type = "text"

}) {

    return (

        <input

            type={type}

            value={value}

            placeholder={placeholder}

            onChange={onChange}

            style={{

                width: "100%",

                padding: "12px",

                borderRadius: 8,

                border: "1px solid #334155",

                background: "#0f172a",

                color: "white",

                marginBottom: 15

            }}

        />

    );

}

export default Input;