export interface FileEditActions {
    file_id: string
    webactions: EditAction[]
}

export interface EditAction {
    type: string
    params: object
}