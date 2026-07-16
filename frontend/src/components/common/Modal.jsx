function Modal({

    title,

    children,

    onClose

}) {

    return (

        <div

            style={{

                position: "fixed",

                top: 0,

                left: 0,

                width: "100%",

                height: "100%",

                background: "rgba(0,0,0,.65)",

                display: "flex",

                justifyContent: "center",

                alignItems: "center",

                zIndex: 9999

            }}

        >

            <div

                style={{

                    width: "900px",

                    maxHeight: "90vh",

                    overflowY: "auto",

                    background: "#111827",

                    borderRadius: 14,

                    border: "1px solid #334155",

                    padding: 30,

                    position: "relative"

                }}

            >

                <button

                    onClick={onClose}

                    style={{

                        position: "absolute",

                        top: 20,

                        right: 20,

                        background: "transparent",

                        border: "none",

                        color: "white",

                        fontSize: 24,

                        cursor: "pointer"

                    }}

                >

                    ✕

                </button>

                <h2

                    style={{

                        color: "white",

                        marginBottom: 25

                    }}

                >

                    {title}

                </h2>

                {children}

            </div>

        </div>

    );

}

export default Modal;