import React from "react"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "../../../UI/Toolbar"
import ThreadsNewButton from "../ThreadsNewButton"

interface IThreadsToolbarProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsToolbar: React.FC<IThreadsToolbarProps> = ({ category }) => (
  <Toolbar>
    <ToolbarSeparator />
    <ToolbarItem>
      <ThreadsNewButton category={category} />
    </ToolbarItem>
  </Toolbar>
)

export default ThreadsToolbar
