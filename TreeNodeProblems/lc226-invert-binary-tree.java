package TreeNodeProblems;

class Solution {
    public static TreeNode invertTree(TreeNode root) {
            if (root == null) return null;
            TreeNode dummy = new TreeNode();
            dummy = root.left;
            root.left = root.right;
            root.right = dummy;
    
            invertTree(root.left);
            invertTree(root.right);
            return root;
    
        }
    }
    
    class Runner {
        public static void main(String[] args) {
            TreeNode root = TreeNode.of(4,2,7,1,3,6,9);
            TreeNode ans = Solution.invertTree(root);
               
    }
}