/**
 * Checks that given object is not null and not undefined. Also checks the same inwards in provided nested keys
 *
 * @example
 *  let check = _hasOwnValue({"foo": {"bar": ""}}, false, true, "foo", "bar");
 *  // check is now false. key "foo" is found, key "bar" is found, but "bar" is emptyString, and params specify to check for them
 *
 * @example
 *  let check = _hasOwnValue({"foo": {"bar": {}}}, true, false, "foo", "bar");
 *  // check is now false. key "foo" is found, key "bar" is found, but "bar" is {}, and params specify to check for emptyObject.
 *
 * @example
 *  let check = _hasOwnValue({"foo": {"bar": {}}}, false, false, "foo", "bar");
 *  // check is now true. key "foo" is found, key "bar" is found, so no requested values are null or undefined.
 *
 *  NOTE: Other functions in this file lets you ignore the boolean params - so just use them :)
 *
 * @param givenObject   The object to validate
 * @param emptyObject   if true - keys mapped to empty object {} will also give false
 * @param emptyString   if true - keys mapped to empty string "" will also give false
 * @param args          nested keys to look for, so to validate myObject.foo.bar call _hasOwnValue(myObject, false, false, "foo". "bar")
 * @returns {boolean}   true if validation passes, false if not.
 */
const _hasOwnValue = function (givenObject, emptyObject, emptyString, ...args) {
    function checkValue(value) {
        return (value != undefined && value != null && (!emptyObject || value != {}) && (!emptyString || value != ""));
    }

    if (!checkValue(givenObject)) {
        return false;
    }

    for (let key of args) {
        if (!(key in givenObject) || !checkValue(givenObject[key])) {
            return false;
        }
        givenObject = givenObject[key];
    }

    return true;
}

/**
 * Validate that an object and nested keys are not null, undefined or empty string "".
 *
 * @example
 * // check that myObject.foo.bar exists:
 * objectHasOwnValueCheckEmptyString(myObject, "foo", "bar")
 *
 * @param givenObject   the object to validate
 * @param args          nested keys to check
 * @returns {boolean}   true if neither the object or any provided nested key is null, undefined or ""
 */
export function objectHasOwnValueCheckEmptyString(givenObject, ...args) {
    return _hasOwnValue(givenObject, false, true, ...args);
}

/**
 * Validate that an object and nested keys are not null, undefined or empty object {}.
 *
 * @example
 * // check that myObject.foo.bar exists:
 * objectHasOwnValueCheckEmptyString(myObject, "foo", "bar")
 *
 * @param givenObject   the object to validate
 * @param args          nested keys to check
 * @returns {boolean}   true if neither the object or any provided nested key is null, undefined or {}
 */
export function objectHasOwnValueCheckEmptyObject(givenObject, ...args) {
    return _hasOwnValue(givenObject, true, false, ...args);
}

/**
 * Validate that an object and nested keys are not null, undefined or empty string "" or empty object {}.
 *
 * @example
 * // check that myObject.foo.bar exists:
 * objectHasOwnValueCheckEmptyString(myObject, "foo", "bar")
 *
 * @param givenObject   the object to validate
 * @param args          nested keys to check
 * @returns {boolean}   true if neither the object or any provided nested key is null, undefined, {} or ""
 */
export function objectHasOwnValueCheckAll(givenObject, ...args) {
    return _hasOwnValue(givenObject, true, true, ...args);
}

/**
 * Validate that an object and nested keys are not null or undefined.
 *
 * @example
 * // check that myObject.foo.bar exists:
 * objectHasOwnValueCheckEmptyString(myObject, "foo", "bar")
 *
 * @param givenObject   the object to validate
 * @param args          nested keys to check
 * @returns {boolean}   true if neither the object or any provided nested key is null or undefined.
 */
export function objectHasOwnValue(givenObject, ...args) {
    return _hasOwnValue(givenObject, false, false, ...args);
}