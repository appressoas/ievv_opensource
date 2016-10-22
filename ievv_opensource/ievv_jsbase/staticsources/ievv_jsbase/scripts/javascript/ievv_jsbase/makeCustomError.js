/**
 * Make a custom error "class".
 *
 * Makes an old style prototype based error class.
 *
 * @param name The name of the error class.
 * @returns {Error} The created error class.
 */
export default function makeCustomError(name) {
    let CustomError = function(message) {
        this.message = message;
        var last_part = new Error().stack.match(/[^\s]+$/);
        this.stack = `${this.name} at ${last_part}`;
    };
    Object.setPrototypeOf(CustomError, Error);
    CustomError.prototype = Object.create(Error.prototype);
    CustomError.prototype.name = name;
    CustomError.prototype.message = "";
    CustomError.prototype.constructor = CustomError;
    return CustomError;
}
